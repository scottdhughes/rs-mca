# M31 varying-G affine-span and shortening route-cut packet

This packet certifies two exact local advances for the Mersenne-31 LIST
boundary residual.

1. Every reconstructed shallow varying-`G` family obeys

   ```text
   sum_i binom(w+s_i+r+e,r) <= binom(R+g-e,r).
   ```

   At the inherited shallow cardinality `15,775,933`, this excludes affine
   ranks one through four, forces `g>=874,886` at rank five and `g>=87,070`
   at rank six, and gives exact weighted excess ceilings through rank ten.
   Rank seven and above remain open; rank eleven receives no uniform cut over
   the full shallow range.

2. Agreement shortening and exact-shell error puncturing close the two old
   fixed-`G` endpoints.  The unresolved ordinary-RS interval shrinks from

   ```text
   72,859 <= m <= 908,270
   ```

   to

   ```text
   72,860 <= m <= 908,269.
   ```

The companion exhaustive Sage scanner also shows in five tiny cells that
mixed-`G` realized lists can be much larger than every fixed-`G` slice.  It
is a toy falsification control, not deployed evidence.

This packet moves no Grande Finale v4 atom and does not close the M31 row.
Its live terminal is
`UNPAID_HIGH_AFFINE_RANK_SPLIT_RATIONAL_INCIDENCE`.

## Replay

From the repository root:

```bash
python3 experimental/scripts/verify_m31_varying_g_affine_span_shortening_route_cut_v1.py
python3 -O experimental/scripts/verify_m31_varying_g_affine_span_shortening_route_cut_v1.py
python3 experimental/scripts/verify_m31_varying_g_affine_span_shortening_route_cut_v1.py --tamper-selftest
sage experimental/scripts/verify_m31_varying_g_affine_span_shortening_route_cut_v1.sage
sage experimental/scripts/scan_m31_varying_g_shallow_incidence_toy_v1.sage --summary-only --pretty
python3 experimental/scripts/verify_m31_varying_g_affine_span_shortening_route_cut_v1.py --check
python3 experimental/scripts/verify_m31_varying_g_affine_span_shortening_route_cut_packet_v1.py
python3 experimental/scripts/verify_m31_varying_g_affine_span_shortening_route_cut_packet_v1.py --tamper-selftest
```

The primary verifier uses explicit exceptions under both normal and optimized
Python, checks the sealed predecessor payloads and all source hashes, and
detects proof-critical hostile mutations.  The Sage replay recomputes the
deployed arithmetic without importing the Python implementation.  The toy
scanner exhausts every printed finite-field cell and separately reports
abstract, fixed-`G`, mixed-`G`, and actually realized maxima.
The packet verifier then replays both sealed predecessor packet verifiers,
checks the closed schema and fresh source hashes, and repeats the scope guards.
