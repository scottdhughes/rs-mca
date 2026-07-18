# M1 KoalaBear tangent first-match owner splice v1

This packet promotes the fixed-SP3 tangent image to a global-once
first-match slope owner for each received pair:

```text
Z_tan = Gamma_in intersect
        {-epsilon_0(x)/epsilon_1(x) : x in Sigma, epsilon_1(x) != 0}
|Z_tan| <= |Sigma| <= j = 981104.
```

The MCA numerator is a maximum over received pairs, so the same uniform cap is
charged once inside each pair-level ledger and then maximized.  The packet does
not union tangent images across received pairs or alternative SP3 translations.

After deleting `Z_tan`, the checker requires a complete selector restart:
global low carrier first, then the high-union small-family cap at `15`, ranks
at most three, ranks four through eight, and then the rebuilt rank-nine coarse
actual-core terminal before the one-cut/atlas route.  All selector-derived
data are stale after the deletion.  The restricted
predecessor selector proves that the new minimum rank is at most nine, but it
does not determine that minimum.

Exact post-charge values are:

```text
U_paid       = 2603484103
B_remaining  = 274980725507910984
T_18014      = 17907571352523
E_max        = 5284472953556748839425672939211329356986005299
K_remaining  = 4807520
```

The tempting value `old_T_18014 - j = 17907571526480` is rejected: after
banking the charge and rebuilding/reselecting, it is too large by `173957`.
The one-cut compiler is invoked only after its predecessor coarse cap fails:
for the full carrier this cap is `1825750153566470657`, strictly above both
the pre-charge and post-charge remaining budgets.  The checker separately
uses the audited paid cell `(N_V,d_V,D)=(1699344,1,0)`, whose coarse cap is
`274980655093567589`, and verifies that the coarse-failure guard itself rejects
that cell before constructing a one-cut threshold.

## Replay

From the repository root:

```bash
python3 -B experimental/scripts/verify_m1_kb_rank9_tangent_owner_splice_v1.py --check
python3 -B -O experimental/scripts/verify_m1_kb_rank9_tangent_owner_splice_v1.py --check
python3 -B experimental/scripts/verify_m1_kb_rank9_tangent_owner_splice_v1.py --tamper-selftest
python3 -B -O experimental/scripts/verify_m1_kb_rank9_tangent_owner_splice_v1.py --tamper-selftest
sage experimental/scripts/verify_m1_kb_rank9_tangent_owner_splice_v1.sage
```

Load-bearing predecessor replays:

```bash
python3 -B experimental/scripts/verify_m1_kb_rank9_zero_pencil_tangent_projection_v1.py --check
python3 -B experimental/scripts/verify_m1_kb_rank9_deployed_source_incidence_contract_v1.py --check
python3 -B experimental/scripts/verify_m1_kb_branch3_5_mask_contract_v1.py --check
python3 -B experimental/scripts/verify_m1_kb_branch3_low_excess_carrier_cut_v1.py --check
python3 -B experimental/scripts/verify_m1_kb_branch3_tdd_excess_v1.py --check
python3 -B experimental/scripts/verify_m1_kb_branch3_actual_core_mds_v1.py --check
python3 -B experimental/scripts/verify_m1_kb_branch3_rank9_mask_deficit_v1.py --check
python3 -B experimental/scripts/verify_kb_mca_1116048_base_slope_universe_v2.py --check
```

The mutation suites are fail-closed golden-object checks, including a mutation
of the predecessor coarse-failure premise.  Their passing count
must not be read as the same number of independent mathematical proofs.  The
top-level checker pins predecessor payloads and selected fields; the separate
commands above execute the eight load-bearing predecessor verifiers.

## Scope

This packet moves only the tangent charge.  It absorbs zero pencils but does
not prove the determinant-weighted nonzero rich-pencil incidence bound, close
rank nine, determine `U_Q` or `U_A`, close the KoalaBear row, authorize rank at
least ten, or promote any result to Lean or a stable paper.
