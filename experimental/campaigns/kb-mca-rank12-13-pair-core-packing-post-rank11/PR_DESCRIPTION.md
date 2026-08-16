# Pull request title

[MCA] Pay affine error ranks twelve and thirteen by pair-core packing

# Pull request body

## Summary

Direct successor to the rank-eleven payment at exact parent
`d01c546f4dca70e256c18c142873821b3bb48ab5`.

For a full shortened row `(R+k,k,d+k)`, distinct complete minimizing-pair
cores meet in at most `k-1` coordinates.  At a deficiency threshold `T`,
Cauchy on the coordinate/core incidence matrix gives

```text
r <= floor(n(h-k+1)/(h^2-n(k-1))), h=m-T,
```

when the denominator is positive.  One fixed pair owns at most `981,105`
finite slopes; high-deficiency slopes are charged to the pointwise margin
resource.

## Exact payments

```text
error rank 12
  descent endpoint K=3       80,415,635
  T=5761 pair-core cap        16,380,678
  slack                       64,034,957

error rank 13
  descent endpoint K=4       73,640,859
  T=12233 pair-core cap       22,658,813
  slack                       50,982,046
```

The cumulative all-deficiency compiler is stronger:

```text
K=3 cap 14,778,066
K=4 cap 15,649,594
```

Restoring the disjoint near-rational charge `134,944` pays both complete
affine-error-rank branches.

## Honest next wall

For error rank fourteen, capped descent reaches rank eight with
`39,342,841,453` slopes, while the cumulative endpoint cap is
`55,071,795,746`.  The method misses by `15,728,954,293`; rank fourteen is
not claimed.

## Scope

- affine error rank 12: paid;
- affine error rank 13: paid;
- affine error rank 14: open;
- active-v4 movement: 0;
- KoalaBear closure: no.

Slope ownership is frozen once by minimizing pair type.  No support or slope
is charged twice.

## Verification

The packet includes exact descent and endpoint modules, a canonical result,
a manifest, full deployed scans, finite Fisher/Cauchy controls, greedy-resource
controls, hostile mutations, an independent reconstruction, and Wolfram exact
replay.  No external theorem is load-bearing.

## Review boundary

- head: `scottdhughes:codex/kb-mca-rank12-13-pair-core-packing-post-rank11`
- exact parent: `d01c546f4dca70e256c18c142873821b3bb48ab5`
