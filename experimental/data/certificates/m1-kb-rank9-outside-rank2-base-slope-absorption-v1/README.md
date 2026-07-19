# M1 KoalaBear outside-rank-two base-slope absorption v1

This packet proves that the 166 moving-root slopes printed in the predecessor
active-source packet are removed at or before the existing global base-slope
owner, before the sparse/rank-nine selector is built. It also freezes the
maximal-gcd projective-subline dichotomy and leaves genuinely extension-valued
and lower-gcd residuals unpaid.

Replay from the repository root:

```bash
python3 -B \
  experimental/scripts/verify_m1_kb_rank9_outside_rank2_base_slope_absorption_v1.py \
  --check
python3 -B \
  experimental/scripts/verify_m1_kb_rank9_outside_rank2_base_slope_absorption_v1.py \
  --tamper-selftest
python3 -B -O \
  experimental/scripts/verify_m1_kb_rank9_outside_rank2_base_slope_absorption_v1.py \
  --check
python3 -B -O \
  experimental/scripts/verify_m1_kb_rank9_outside_rank2_base_slope_absorption_v1.py \
  --tamper-selftest

HOME=/tmp/sage-home /usr/local/bin/sage \
  experimental/scripts/verify_m1_kb_rank9_outside_rank2_base_slope_absorption_v1.sage

python3 -B \
  experimental/scripts/verify_kb_mca_1116048_base_slope_universe_v2.py \
  --check
python3 -B \
  experimental/scripts/verify_kb_mca_1116048_base_slope_universe_v2.py \
  --tamper-selftest
python3 -B \
  experimental/scripts/verify_m1_kb_rank9_active_source_matroid_reindex_v1.py \
  --check
python3 -B \
  experimental/scripts/verify_m1_kb_rank9_active_source_matroid_reindex_v1.py \
  --tamper-selftest
```

Expected main terminal:

```text
M1 outside-rank-two base-slope absorption: PASS
```

The certificate records zero ledger movement. The base-field charge was
already banked globally; this packet corrects ownership and narrows the live
rank-two residual to genuinely extension-defined sublines and lower-gcd
rational maps.
