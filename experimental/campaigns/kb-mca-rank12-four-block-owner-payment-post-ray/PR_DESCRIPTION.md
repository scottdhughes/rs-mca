## Summary

Stacked on exact parent
`ea0541ca0cafb49ca79ff48c1285887344e1103b`.

This PR strengthens the rank-twelve large-locator proper-drop payment from
`K>=858,619` to

```text
K>=662,480.
```

For a proper rank-two leaf, slopes whose frozen supports meet the actual full
common pair core form one rank-one family and cost at most `4,070,947`.
Among supports avoiding the core, four slopes witness every genuinely
two-dimensional residual. Their omission sets induce four clean projective
fibers. Every further slope is assigned exactly once to:

- one of at most four triplet/base-slope owners;
- one fixed codeword-pair owner determined by two clean equations; or
- one universal-core-aware correction ray determined by one clean equation.

The triplet consistency determinant is affine in the slope with nonzero
Vandermonde leading coefficient, so there is no identity-triplet branch.

The exact first paying cell is

```text
ambient K                     662,480
effective rank-one k           75,757
common-locator floor          586,723
omission size r               394,381
pair/triplet cap              629,630
two-ray cap                   470,330
exceptional cap             1,099,960
rank-one cap                4,070,947
proper-drop total           5,170,907
rank-two load               5,170,912
slack                                5
```

Hence a proper drop is impossible for every
`662,480<=K<=1,048,576`. The complete `5,170,912`-slope rank-two family
shortens intact through all `386,097` top dimensions and reaches
`K<=662,479`.

## Exact adjacent wall

At `K=662,479`, the same floor-safe compiler gives total `5,170,930`, which
is `18` above the load. This is a method wall, not an unsafe certificate.
The extremal relaxed profile has two active one-block correction rays and one
dominant fixed-pair owner; the next theorem must couple them and save at least
`19` slopes.

## Scope

- proper rank-two drops for `K>=662,480`: paid;
- affine error rank twelve: not paid;
- active-v4 ledger movement: `0`;
- KoalaBear closure: not claimed.

The proof uses a chronology-disjoint support partition. It does not sum local
locator certificates or overlapping owners.

## Verification

- exact scan of all deployed ambient cells: PASS;
- exact rational ray arithmetic: PASS;
- independent implementation: PASS;
- finite-field triplet rigidity cells: `1,460`;
- small dirty-incidence profiles: `767,038`;
- hostile mutations: `8/8` rejected;
- Wolfram boundary and convexity replay: PASS;
- literature/source-scope audit: GREEN;
- manifest and file hashes: PASS.

Canonical payload is recorded in the sealed manifest.
