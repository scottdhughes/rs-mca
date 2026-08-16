# Pull request title

[MCA] Make the nested rank-eleven pins source-bound shortening coordinates

# Pull request body

## Summary

Stacked successor to the nested pinned-span packet at exact parent
`42e15d1bc6d8c2f1b73936bea157f6fcfafbfb08`, which is itself stacked directly on PR #1173.

The parent proves one nested chain of common coordinates and direction spaces,
but deliberately stops before asserting that the pins can be used as actual
support-wise MCA shortening coordinates.  This PR supplies that missing
source theorem.

For each bad slope, use its complete scalar agreement domain.  That complete
domain contains the original exact bad support and is therefore itself
pair-noncontained.  Subtract one fixed degree-`<10` interpolation pair on
`T_10`, divide by the locator of each prefix `T_k`, and delete those
coordinates.  Any simultaneous pair explanation in the shortened row lifts
to a simultaneous pair explanation on the complete original domain, a
contradiction.

Consequently, for every `1<=k<=10`, the parent family becomes an actual
support-wise MCA-bad family in

```text
(n_k,K_k,m_k)=(2097152-k,1048576-k,1116048-k).
```

The slopes and direction dimensions are preserved.  The ten loads/dimensions
remain

```text
k   assigned load             quotient dimension at least
1   2,843,853,816,476,423      8
2      93,708,171,878,891      7
3       3,087,708,134,499      6
4         101,738,094,101      5
5           3,352,119,806      3
6             110,444,488      2
7               3,638,792      2
8                 119,884      2
9                   3,950      2
10                    131      2
```

The quotient spaces form a compatible ladder:

```text
(X-x_(k+1)) * V'_(k+1) <= V'_k.
```

All shortened rows retain exactly

```text
n_k-K_k = 1,048,576
m_k-K_k =    67,472
n_k-m_k =   981,104.
```

## Essential semantic repair

The theorem does **not** swap pinned coordinates into arbitrary exact witness
supports.  A shipped `GF(5)` example proves that such a swap can turn a bad
support into a pair-contained support.  Complete agreement domains and the
lift argument are essential.

## Scope

- source-bound shortening ladder: proved;
- compatible quotient-direction ladder: proved;
- active-v4 ledger movement: `0`;
- rank-eleven payment: no;
- KoalaBear closure: no.

The ten loads are nested and are not summed.

## Verification

- primary exact verifier: PASS
- independent polynomial-arithmetic audit: PASS
- hostile mutations: PASS
- exhaustive `GF(5)` support-replacement counterexample: PASS
- exhaustive small locator quotient/lift control: PASS
- Wolfram exact ten-row replay: PASS
- mathematics audit: GREEN
- certificate/custody review: GREEN
- literature sweep: no external theorem is load-bearing

## Dependency and next theorem

This PR must integrate after the nested pinned-span packet at `42e15d1bc6d8c2f1b73936bea157f6fcfafbfb08`.

The strongest next attack is now genuinely algebraic rather than semantic:
apply the relative-order-32, correction-space, Wronskian, or
Sylvester/subresultant machinery to the compatible quotient ladder, beginning
with the `2.84e15`-slope dimension-at-least-eight first shortened family.

## Review boundary

- head repository: `scottdhughes/rs-mca`
- exact parent: `42e15d1bc6d8c2f1b73936bea157f6fcfafbfb08`
