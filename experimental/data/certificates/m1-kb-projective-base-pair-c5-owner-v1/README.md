# M1 KoalaBear projective-base-pair C5 owner v1

This packet banks the pair-global \(F_{\rm proj}=\mathbf F_p\) C5 cell as a
joint distinct-slope owner with the existing residual base-slope bucket.  Its
uniform cap is \(p+1\), replacing the old \(p\) block for exact ledger
movement \(+1\).  It also absorbs the predecessor's full-outside split
maximal-gcd subcell \(c_L=k-2\), while leaving nonsplit/nonbase maximal-gcd,
field-full local-subline, and lower-gcd rational-map routes open.

Replay from the repository root:

```bash
python3 -B \
  experimental/scripts/verify_m1_kb_projective_base_pair_c5_owner_v1.py \
  --check
python3 -B \
  experimental/scripts/verify_m1_kb_projective_base_pair_c5_owner_v1.py \
  --tamper-selftest
python3 -B -O \
  experimental/scripts/verify_m1_kb_projective_base_pair_c5_owner_v1.py \
  --check
python3 -B -O \
  experimental/scripts/verify_m1_kb_projective_base_pair_c5_owner_v1.py \
  --tamper-selftest

HOME=/tmp/sage-home /usr/local/bin/sage \
  experimental/scripts/verify_m1_kb_projective_base_pair_c5_owner_v1.sage

python3 -B \
  experimental/scripts/verify_m1_kb_rank9_outside_rank2_base_slope_absorption_v1.py \
  --check
python3 -B \
  experimental/scripts/verify_m1_kb_rank9_outside_rank2_base_slope_absorption_v1.py \
  --tamper-selftest
python3 -B \
  experimental/scripts/verify_m1_fp2_post_c5_mask_incidence_v1.py \
  --check
python3 -B \
  experimental/scripts/verify_m1_fp2_post_c5_mask_incidence_v1.py \
  --tamper-selftest
python3 -B \
  experimental/scripts/verify_m1_kb_rank9_tangent_owner_splice_v1.py \
  --check
python3 -B \
  experimental/scripts/verify_m1_kb_rank9_tangent_owner_splice_v1.py \
  --tamper-selftest
python3 -B \
  experimental/scripts/verify_kb_mca_1116048_base_slope_universe_v2.py \
  --check
python3 -B \
  experimental/scripts/verify_kb_mca_1116048_base_slope_universe_v2.py \
  --tamper-selftest
```

Expected main terminal:

```text
M1 projective-base-pair C5 owner: PASS
```

The exact \(\mathbf F_{5^6}\) control has six finite slopes on a nonstandard
\(\mathbf F_5\)-subline, of which five are degree six, while the pair remains
globally projectively base-defined.  This shows why the safe finite-chart cap
is \(p+1\) and why raw extension coordinates are not a post-C5 obstruction.
An exact \(\mathbf F_{11^2}\) countercontrol has
\(\deg\gcd(P,Q)=k-2\) but no domain common roots and full projective syndrome
field, guarding the retained nonsplit maximal-gcd terminal.
