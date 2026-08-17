# Rank-twelve large-locator correction-ray payment

This packet is stacked on exact parent
`ed556ccb7527e1c54e58b8d151ccefd8539000ac`.

It combines the parent common-locator floor with a source-bound six-support
synchronization theorem and a new universal-core-aware payment for the
resulting affine correction ray.

## Exact result

For every ambient dimension

```text
858,619 <= K <= 1,048,576
```

a proper rank-two drop is impossible.  The complete rank-two family of
`5,170,912` slopes therefore shortens intact through all `189,958` dimensions
and reaches `K <= 858,618`.

The load-bearing bounds are

```text
rank-one global cap          4,070,947
single affine-ray cap          796,620
--------------------------------------
proper-drop cap              4,867,567
rank-two load                5,170,912
slack                          303,345
```

The rank-one cap is deliberately the global all-dimension maximum.  Using the
smaller capacity at the minimum locator floor would be invalid because a
larger actual common core can lower the effective dimension and increase the
rank-one capacity.

## Replay

```bash
python3 experimental/scripts/verify_kb_mca_rank12_large_locator_ray_payment_v1.py
python3 experimental/scripts/verify_kb_mca_rank12_large_locator_ray_payment_v1.py --tamper-selftest
python3 experimental/scripts/audit_kb_mca_rank12_large_locator_ray_payment_v1.py
python3 experimental/scripts/verify_kb_mca_rank12_large_locator_ray_payment_manifest_v1.py
```

## Nonclaims

- affine error rank twelve is not paid;
- active-v4 ledger movement is zero;
- KoalaBear closure is not claimed;
- the adjacent `K=858,618` near-minimum-weight obstruction remains open.
