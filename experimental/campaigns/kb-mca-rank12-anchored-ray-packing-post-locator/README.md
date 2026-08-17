# Rank-twelve anchored correction-ray packing

## Exact parent

This packet is stacked directly on
`ed556ccb7527e1c54e58b8d151ccefd8539000ac`, the source-bound rank-twelve
common-locator-floor packet.

## Result

Every proper rank-two drop in the ambient interval

```text
706,612 <= K <= 1,048,576
```

is impossible.  Hence the complete rank-two family of `5,170,912` slopes
shortens intact through `341,965` ambient dimensions and reaches

```text
K <= 706,611.
```

The proof uses two new ingredients.

1. **Anchored ray packing.**  Two fixed exceptional slopes turn every other
   explanation into a normalized second divided difference.  Distinct
   normalized values have disjoint triple-agreement sets; otherwise two
   independent direction words vanish at one coordinate and create a forbidden
   whole-family pair core.  Thus the number of correction rays is at most

   \[
   \left\lfloor\frac{N-2r}{N-3r}\right\rfloor.
   \]

   The parent floor makes this at most four exactly from `K=706,612` onward.

2. **Universal-core-aware weighted-ray payment.**  After cancelling any
   universal core internal to one ray, the remaining coordinates form a
   weighted affine-line arrangement of total weight `M+r` and threshold `M`,
   where `M>=D+1`.  Parity convexity reduces the unknown `M` to a finite
   endpoint table.  The largest ray bound needed is `627,362`.

Exact branch accounting:

```text
ray count   certified cap   slack to 5,170,912
1             4,460,342            710,570
2             4,908,361            262,551
3             4,425,931            744,981
4             4,937,277            233,635
```

## Adjacent wall

At `K=706,611`, the anchored packing ratio is

```text
floor(430045 / 86007) = 5.
```

The direct five-ray envelope is `5,417,198`, over the rank-two load by
`246,286`.  This is a method wall, not an unsafe certificate.

## Verification

```bash
python3 experimental/scripts/verify_kb_mca_rank12_anchored_ray_packing_v1.py
python3 experimental/scripts/verify_kb_mca_rank12_anchored_ray_packing_v1.py --tamper-selftest
python3 experimental/scripts/audit_kb_mca_rank12_anchored_ray_packing_v1.py
python3 experimental/scripts/verify_kb_mca_rank12_anchored_ray_packing_manifest_v1.py
```

## Scope

- proper-drop branch for `K>=706,612`: paid;
- affine error rank twelve: not paid;
- active-v4 ledger movement: `0`;
- KoalaBear closure: not claimed.
