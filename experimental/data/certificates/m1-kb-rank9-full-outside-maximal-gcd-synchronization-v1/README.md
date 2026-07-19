# M1 KoalaBear full-outside maximal-gcd synchronization v1

This packet proves a conditional three-point synchronization theorem for one
fixed source-bound complete selector.  Every full-outside, rank-two rich line
whose full gcd has degree `k-2` has the same reduced Möbius map, so its
deduplicated finite selected slopes have cap `p+1`.

The current repository has no deployed complete-selector terminal inventory
or full producer validator.  The certificate therefore retains
`UNBOUND_COMPLETE_SELECTOR_MAXIMAL_GCD_PROVENANCE`, records the prospective
owner arithmetic separately, and moves the deployed ledger by zero.

Replay from the repository root:

```bash
python3 -B \
  experimental/scripts/verify_m1_kb_rank9_full_outside_maximal_gcd_synchronization_v1.py \
  --check
python3 -B \
  experimental/scripts/verify_m1_kb_rank9_full_outside_maximal_gcd_synchronization_v1.py \
  --tamper-selftest
python3 -B -O \
  experimental/scripts/verify_m1_kb_rank9_full_outside_maximal_gcd_synchronization_v1.py \
  --check
python3 -B -O \
  experimental/scripts/verify_m1_kb_rank9_full_outside_maximal_gcd_synchronization_v1.py \
  --tamper-selftest

HOME=/tmp/sage-home /usr/local/bin/sage \
  experimental/scripts/verify_m1_kb_rank9_full_outside_maximal_gcd_synchronization_v1.sage
```

Predecessor replays:

```bash
python3 -B experimental/scripts/verify_m1_kb_projective_base_pair_c5_owner_v1.py --check
python3 -B experimental/scripts/verify_m1_kb_projective_base_pair_c5_owner_v1.py --tamper-selftest
python3 -B experimental/scripts/verify_m1_kb_rank9_outside_rank2_base_slope_absorption_v1.py --check
python3 -B experimental/scripts/verify_m1_kb_rank9_outside_rank2_base_slope_absorption_v1.py --tamper-selftest
python3 -B experimental/scripts/verify_m1_kb_rank9_active_source_matroid_reindex_v1.py --check
python3 -B experimental/scripts/verify_m1_kb_rank9_active_source_matroid_reindex_v1.py --tamper-selftest
python3 -B experimental/scripts/verify_m1_kb_rank9_projective_source_load_v1.py --check
python3 -B experimental/scripts/verify_m1_kb_rank9_projective_source_load_v1.py --tamper-selftest
python3 -B experimental/scripts/verify_m1_kb_branch3_rank9_rich_pencil_atlas_v1.py --check
python3 -B experimental/scripts/verify_m1_kb_branch3_rank9_rich_pencil_atlas_v1.py --tamper-selftest
python3 -B experimental/scripts/verify_m1_kb_rank9_deployed_source_incidence_contract_v1.py --check
python3 -B experimental/scripts/verify_m1_kb_rank9_deployed_source_incidence_contract_v1.py --tamper-selftest
```

Expected main terminal:

```text
M1 full-outside maximal-gcd synchronization: PASS
```

The Sage replay uses two distinct nonbase degree-four gcd factors over
`GF(5^6)` which agree at three source anchors.  It also checks a pole and a
two-anchor countercontrol.  These are exact toy controls, not deployed
selector evidence.
