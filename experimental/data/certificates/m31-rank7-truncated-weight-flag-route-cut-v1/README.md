# M31 rank-seven truncated-weight/flag route-cut certificate

This packet proves a rank-uniform truncated generalized-weight inequality and
uses it to pay both exact rank-seven union flanks.  It leaves the primitive
middle

```text
72428 <= g <= 354998
```

open.  It moves no Grande Finale v4 atom and does not close rank seven, any
higher rank, or the M31 LIST row.

The immediate dependency is the rank-six closure packet with payload

```text
3e0a6102795f88aa8121229bc40bcc723aa7e5cc81bbcfd5b0013adf5d11caf9
```

## Replay

From the repository root:

```bash
python3 experimental/scripts/verify_m31_rank7_truncated_weight_flag_route_cut_v1.py --check
python3 -O experimental/scripts/verify_m31_rank7_truncated_weight_flag_route_cut_v1.py --check
python3 experimental/scripts/verify_m31_rank7_truncated_weight_flag_route_cut_v1.py --tamper-selftest
sage experimental/scripts/verify_m31_rank7_truncated_weight_flag_route_cut_v1.sage
python3 experimental/scripts/verify_m31_rank7_truncated_weight_flag_route_cut_packet_v1.py
python3 experimental/scripts/verify_m31_rank7_truncated_weight_flag_route_cut_packet_v1.py --tamper-selftest
```

To regenerate the canonical manifest after an intentional source change:

```bash
python3 experimental/scripts/verify_m31_rank7_truncated_weight_flag_route_cut_packet_v1.py --write-manifest
```

Then rerun the full packet verifier and tamper self-test.

## Exact result

- Common-zero Johnson pays every rank-seven union `67454..72427`.
- Truncated-weight/codimension-one pays every union `354999..1116023`.
- The exact residual has 282,571 union sizes, `72428..354998`.
- The low 432 values require a mixed-locator near-MDS theorem after fixed-`G`
  owners are removed.
- The remaining interval contains the deterministic punctured ordinary-RS
  middle and cannot be closed by assuming locator variation.

The `GF(11)` Sage family is an exact orientation and sharpness control for
the truncated-basis theorem.  It is not deployed evidence.
