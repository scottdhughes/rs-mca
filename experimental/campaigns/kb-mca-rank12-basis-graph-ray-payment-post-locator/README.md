# Rank-twelve basis-graph correction-ray payment

This packet is stacked on exact parent
`ed556ccb7527e1c54e58b8d151ccefd8539000ac`.

It replaces the archived six-support synchronization packet by using adjacent
bases in the quotient rank-three matroid. Adjacent bases share two slopes, so
only four omission sets—not six—enter the minimum-distance comparison.
Basis-graph connectivity then synchronizes every nonzero vector second
divided difference into one affine correction ray.

## Exact payment

```text
unconditional interval     778,970 <= K <= 1,048,576
ambient dimensions paid                         269,607
rank-one global cap                           4,070,947
single-ray cap                                1,067,271
proper-drop cap                               5,138,218
rank-two load                                 5,170,912
minimum slack                                    32,694
```

Every proper rank-two drop in that interval is impossible, so the full
`5,170,912`-slope family shortens intact to `K<=778,969`.

## Sharpened residual

For `774,075<=K<=778,969`, the synchronized-ray branch is still paid. A
surviving proper drop must therefore emit one nonzero near-MDS basis-edge
word. At `K=778,969`, its residual factor has degree at most three. At the
preceding arithmetic wall `K=774,074`, the synchronized-ray total exceeds the
load by exactly one.

## Replay

```bash
python3 experimental/scripts/verify_kb_mca_rank12_basis_graph_ray_payment_v1.py
python3 experimental/scripts/verify_kb_mca_rank12_basis_graph_ray_payment_v1.py --tamper-selftest
python3 experimental/scripts/audit_kb_mca_rank12_basis_graph_ray_payment_v1.py
python3 experimental/scripts/verify_kb_mca_rank12_basis_graph_ray_payment_manifest_v1.py
```

## Nonclaims

- affine error rank twelve is not paid;
- active-v4 ledger movement is zero;
- KoalaBear closure is not claimed.
